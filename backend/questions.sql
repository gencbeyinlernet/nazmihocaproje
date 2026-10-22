-- Run in a dedicated Supabase project. Auth users and Storage are not exposed here.
create table if not exists public.merak_qa_admins(user_id uuid primary key references auth.users(id) on delete cascade);
create table if not exists public.merak_private_questions(
 id uuid primary key default gen_random_uuid(),
 token_hash text unique not null,
 grade_id text not null check(grade_id in ('4','5','6','7','8','9','10','11','12')),
 topic_id text not null default '',
 question text not null check(length(btrim(question)) between 10 and 1500),
 answer text check(length(answer) between 1 and 4000),
 created_at timestamptz not null default now(),
 replied_at timestamptz,
 replied_by uuid references auth.users(id)
);
alter table public.merak_qa_admins enable row level security;
alter table public.merak_private_questions enable row level security;
revoke all on public.merak_qa_admins, public.merak_private_questions from public,anon,authenticated;
-- No anonymous SELECT policy, table grants or public question list.
create or replace function public.merak_qa_is_admin() returns boolean
language sql stable security definer set search_path=public
as $$select auth.uid() is not null and exists(select 1 from public.merak_qa_admins where user_id=auth.uid());$$;
revoke all on function public.merak_qa_is_admin() from public,anon;
grant execute on function public.merak_qa_is_admin() to authenticated;
create or replace function public.merak_question_create(p_grade text,p_topic text,p_question text,p_token text) returns jsonb
language plpgsql security definer set search_path=public as $$
declare new_id uuid;
begin
 if p_grade is null or p_grade not in ('4','5','6','7','8','9','10','11','12') or p_token is null or p_token !~ '^[a-f0-9]{64}$'
 or p_question is null or length(btrim(p_question)) not between 10 and 1500
 or p_topic is null or length(p_topic)>100 or (p_topic<>'' and p_topic !~ ('^g'||p_grade||'-[0-9]+(-[0-9]+)*$'))
 then raise exception 'Invalid question' using errcode='23514';end if;
 perform pg_advisory_xact_lock(734093);
 if (select count(*) from public.merak_private_questions where created_at>now()-interval '24 hours')>=500
 then raise exception 'Question limit reached' using errcode='P0001';end if;
 insert into public.merak_private_questions(token_hash,grade_id,topic_id,question)
 values(encode(sha256(convert_to(p_token,'UTF8')),'hex'),p_grade,p_topic,btrim(p_question)) returning id into new_id;
 return jsonb_build_object('id',new_id);
end $$;
revoke all on function public.merak_question_create(text,text,text,text) from public;
grant execute on function public.merak_question_create(text,text,text,text) to anon,authenticated;
create or replace function public.merak_question_reply(p_token text) returns jsonb
language plpgsql stable security definer set search_path=public as $$
declare result jsonb;
begin
 if p_token is null or p_token !~ '^[a-f0-9]{64}$' then raise exception 'Invalid code' using errcode='23514';end if;
 select jsonb_build_object('question',question,'answer',answer,'replied_at',replied_at,'grade_id',grade_id)
 into result from public.merak_private_questions where token_hash=encode(sha256(convert_to(p_token,'UTF8')),'hex');
 return result;
end $$;
revoke all on function public.merak_question_reply(text) from public;
grant execute on function public.merak_question_reply(text) to anon,authenticated;
create or replace function public.merak_question_admin_list() returns jsonb
language plpgsql stable security definer set search_path=public as $$
begin
 if not public.merak_qa_is_admin() then raise exception 'Admin required' using errcode='42501';end if;
 return coalesce((select jsonb_agg(to_jsonb(q)) from (select id,grade_id,topic_id,question,answer,created_at,replied_at from public.merak_private_questions order by (answer is null) desc,created_at desc limit 200) q),'[]'::jsonb);
end $$;
revoke all on function public.merak_question_admin_list() from public,anon;
grant execute on function public.merak_question_admin_list() to authenticated;
create or replace function public.merak_question_answer(p_id uuid,p_answer text) returns void
language plpgsql security definer set search_path=public as $$
begin
 if not public.merak_qa_is_admin() then raise exception 'Admin required' using errcode='42501';end if;
 if p_answer is null or length(btrim(p_answer)) not between 1 and 4000 then raise exception 'Invalid answer' using errcode='23514';end if;
 update public.merak_private_questions set answer=btrim(p_answer),replied_at=now(),replied_by=auth.uid() where id=p_id;
 if not found then raise exception 'Question not found' using errcode='P0002';end if;
end $$;
revoke all on function public.merak_question_answer(uuid,text) from public,anon;
grant execute on function public.merak_question_answer(uuid,text) to authenticated;

create table users
(
    name text,
    pass text
);

alter table users
    owner to postgres;

INSERT INTO public.users (name, pass) VALUES ('admin', 'c4ca4238a0b923820dcc509a6f75849b');
INSERT INTO public.users (name, pass) VALUES ('user', 'c81e728d9d4c2f636f067f89cc14862c');
create table book
(
    name text,
    id   integer not null
        constraint book_pk
            primary key
);

alter table book
    owner to postgres;

INSERT INTO public.book (name, id) VALUES ('Язык программирования Go', 10);
INSERT INTO public.book (name, id) VALUES ('Язык программирования С', 20);
INSERT INTO public.book (name, id) VALUES ('Семь баз данных за семь недель', 30);
INSERT INTO public.book (name, id) VALUES ('Распределенные системы', 40);
INSERT INTO public.book (name, id) VALUES ('Redis in Action', 50);
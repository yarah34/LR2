create table author
(
    name text,
    id   integer not null
        constraint author_pkey
            primary key
);

alter table author
    owner to postgres;

INSERT INTO public.author (name, id) VALUES ('Брайан Керниган', 1);
INSERT INTO public.author (name, id) VALUES ('Деннис Ритчи', 2);
INSERT INTO public.author (name, id) VALUES ('Уилсон Редмонд', 3);
INSERT INTO public.author (name, id) VALUES ('Эндрю Таненбаум', 4);
INSERT INTO public.author (name, id) VALUES ('Josiah L Carlson', 5);
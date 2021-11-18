create table books_by_authors
(
    id  integer not null
        constraint books_by_authors_pk
            primary key,
    aid integer
        constraint fk_a
            references author,
    bid integer
        constraint fk_b
            references book
);

alter table books_by_authors
    owner to postgres;

INSERT INTO public.books_by_authors (id, aid, bid) VALUES (1000, 1, 10);
INSERT INTO public.books_by_authors (id, aid, bid) VALUES (2000, 1, 20);
INSERT INTO public.books_by_authors (id, aid, bid) VALUES (3000, 2, 20);
INSERT INTO public.books_by_authors (id, aid, bid) VALUES (4000, 3, 30);
INSERT INTO public.books_by_authors (id, aid, bid) VALUES (5000, 4, 40);
INSERT INTO public.books_by_authors (id, aid, bid) VALUES (6000, 5, 50);
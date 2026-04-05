travel(a, b, car).
travel(b, c, car).
travel(c, d, car).
travel(d, e, car).
travel(e, f, car).

travel(j, k, car).
travel(k, l, car).
travel(l, m, car).
travel(m, n, car).
travel(n, o, car).

travel(s, t, car).
travel(t, u, car).
travel(u, v, car).
travel(v, w, car).
travel(w, x, car).

travel(e, h, train).
travel(h, k, train).
travel(k, n, train).
travel(n, q, train).
travel(q, t, train).

travel(a, f, plane).
travel(f, k, plane).
travel(k, p, plane).
travel(p, u, plane).
travel(u, z, plane).

travel(FROM, TO) :- travel(FROM, TO, _).
travel(FROM, TO) :- travel(FROM, STOP, _), travel(STOP, TO).

path(FROM, TO, [travel(FROM, TO, BY)]) :- travel(FROM, TO, BY).
path(FROM, TO, [travel(FROM, STOP, BY) | REST]) :- travel(FROM, STOP, BY), path(STOP, TO, REST).
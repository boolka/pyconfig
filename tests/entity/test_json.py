from pyconfig.entry.json import JsonEntry


def test_get():
    with open("./tests/entity/testdata/config.json", "rb") as f:
        e = JsonEntry(f)

        assert e.get("num") == 1
        assert e.get("f_num") == 1.0
        assert e.get("e_num") == 1e2
        assert e.get("bool") is True
        assert e.get("n_arr") == [1, 2, 3]
        assert e.get("s_arr") == ["1", "2", "3"]
        assert e.get("str") == '"custom string"\n'

        assert e.get("obj.num") == 1
        assert e.get("obj.f_num") == 1.0
        assert e.get("obj.e_num") == 1e2
        assert e.get("obj.bool") is True
        assert e.get("obj.n_arr") == [1, 2, 3]
        assert e.get("obj.s_arr") == ["1", "2", "3"]
        assert e.get("obj.str") == '"custom string"\n'


def test_get_unknown():
    with open("./tests/entity/testdata/config.json", "rb") as f:
        e = JsonEntry(f)
        assert e.get("unknown") is None
        assert e.get("obj.unknown") is None

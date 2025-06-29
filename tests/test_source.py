from socket import gethostname

from pytest import raises

from pyconfig.source import EntrySource, InvalidSourceInstance, parse_filename


def test_valid_filenames():
    assert parse_filename("default") == (EntrySource.def_src, None, None)
    assert parse_filename("default-1") == (EntrySource.def_inst_src, None, 1)
    assert parse_filename("local") == (EntrySource.loc_src, None, None)
    assert parse_filename("local-1") == (EntrySource.loc_inst_src, None, 1)
    assert parse_filename("local-production") == (
        EntrySource.loc_dep_src,
        "production",
        None,
    )
    assert parse_filename("local-development-1") == (
        EntrySource.loc_dep_inst_src,
        "development",
        1,
    )
    assert parse_filename(gethostname(), gethostname()) == (
        EntrySource.host_src,
        None,
        None,
    )
    assert parse_filename(f"{gethostname()}-1", gethostname()) == (
        EntrySource.host_inst_src,
        None,
        1,
    )
    assert parse_filename(f"{gethostname()}-testing", gethostname()) == (
        EntrySource.host_dep_src,
        "testing",
        None,
    )
    assert parse_filename("env") == (EntrySource.env_src, None, None)
    assert parse_filename("production") == (EntrySource.dep_src, None, None)
    assert parse_filename("stage-1") == (EntrySource.dep_inst_src, "stage", 1)


def test_odd_filenames():
    assert parse_filename("asdf") == (EntrySource.dep_src, None, None)
    assert parse_filename("asdf-1") == (EntrySource.dep_inst_src, "asdf", 1)

    with raises(InvalidSourceInstance):
        assert parse_filename("asdf-asdf-1") == (EntrySource.host_inst_src)

    assert parse_filename("asdf-asdf-asdf") == (EntrySource.dep_src, None, None)

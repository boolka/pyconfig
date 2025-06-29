from enum import IntEnum
from re import compile


class InvalidSourceInstance(Exception):
    pass


class EntrySource(IntEnum):
    def_src = 1
    def_inst_src = 2
    dep_src = 3
    dep_inst_src = 4
    host_src = 5
    host_inst_src = 6
    host_dep_src = 7
    host_dep_inst_src = 8
    loc_src = 9
    loc_inst_src = 10
    loc_dep_src = 11
    loc_dep_inst_src = 12
    env_src = 13


re_def_inst = compile(r"^default-\d+$")
re_loc_inst = compile(r"^local-\d+$")
re_loc_dep = compile(r"^local-\w+$")
re_loc_dep_inst = compile(r"^local-\w+-\d+$")

re_inst = compile(r"^(\d+)$")
re_word_inst = compile(r"^(.+)-(\d+)$")


def parse_filename(
    filename: str, hostname: str | None = None
) -> tuple[EntrySource, str | None, int | None]:
    file_split = filename.split("-")

    try:
        if filename == hostname:
            return EntrySource.host_src, None, None
        elif filename == "default":
            return EntrySource.def_src, None, None
        elif re_def_inst.match(filename):
            return EntrySource.def_inst_src, None, int(file_split[1])
        elif filename == "local":
            return EntrySource.loc_src, None, None
        elif re_loc_inst.match(filename):
            return EntrySource.loc_inst_src, None, int(file_split[1])
        elif re_loc_dep.match(filename):
            return EntrySource.loc_dep_src, file_split[1], None
        elif re_loc_dep_inst.match(filename):
            return EntrySource.loc_dep_inst_src, file_split[1], int(file_split[2])
        elif filename == "env":
            return EntrySource.env_src, None, None
        elif hostname is not None and hostname in filename:
            omit_hostname = filename.removeprefix(hostname + "-")
            file_split = omit_hostname.split("-")

            if re_inst.match(omit_hostname):
                return EntrySource.host_inst_src, None, int(file_split[0])
            elif re_word_inst.match(omit_hostname):
                return EntrySource.host_dep_inst_src, file_split[0], int(file_split[1])
            else:
                return EntrySource.host_dep_src, file_split[0], None
        elif re_word_inst.match(filename):
            return EntrySource.dep_inst_src, file_split[0], int(file_split[1])
    except ValueError:
        raise InvalidSourceInstance

    return EntrySource.dep_src, None, None

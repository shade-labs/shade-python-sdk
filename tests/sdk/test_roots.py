from pathlib import Path

from shade import ShadeRemote

dummy_path = Path('/not/a/real/path')


server = ShadeRemote(
    Path("/"),
    Path("/"),
    ip='http://localhost'
)


def test_roots():
    id_ = server.roots.add_new_root(dummy_path)

    assert id_ is not None

    assert any(root.id == id_ for root in server.roots.get_roots())

    server.roots.delete_root(id_)

    assert not any(root.id == id_ for root in server.roots.get_roots())

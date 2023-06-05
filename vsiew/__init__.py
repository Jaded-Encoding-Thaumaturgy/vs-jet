# flake8: noqa

import sys
import inspect
from typing import TYPE_CHECKING

update_check = False


if TYPE_CHECKING:
    __all__ = [
        'tools',
        'pyplugin',
        'kernels',
        'exprs',
        'rg',
        'masks',
        'aa',
        'scale',
        'denoise',
        'dehalo',
        'deband',
        'deint',
        'source',

        'vs', 'core'
    ]

    import vsaa as aa
    import vsdeband as deband
    import vsdehalo as dehalo
    import vsdeinterlace as deint
    import vsdenoise as denoise
    import vsexprtools as exprs
    import vskernels as kernels
    import vsmasktools as masks
    import vsrgtools as rg
    import vsscale as scale
    import vssource as source
    import vstools as tools
    from vstools import core, vs
else:
    __all__ = []

c_frame = [inspect.currentframe()]
while (t := c_frame[-1] and c_frame[-1].f_back):
    c_frame.append(t)

    if (
        'self' in t.f_locals and type(t.f_locals['self']).__name__ == 'EntryPoint'
        and t.f_locals['self'].value == 'vsiew:update_packages'
    ) or (
        'pkg_main_name' in t.f_locals and t.f_locals['pkg_main_name'] == 'vsiew.__main__'
    ):
        update_check = True
        break


if update_check:
    __all__.append('update_packages')

    # vsiew
    def update_packages() -> None:
        from .init import update
        update(sys.argv[1:] if sys.argv else None)
else:
    import vsaa as aa
    import vsdeband as deband
    import vsdehalo as dehalo
    import vsdeinterlace as deint
    import vsdenoise as denoise
    import vsexprtools as exprs
    import vskernels as kernels
    import vsmasktools as masks
    import vsrgtools as rg
    import vsscale as scale
    import vssource as source
    import vstools as tools
    from vstools import core, vs

    __all__.extend([
        'tools',
        'pyplugin',
        'kernels',
        'exprs',
        'rg',
        'masks',
        'aa',
        'scale',
        'denoise',
        'dehalo',
        'deband',
        'deint',
        'source',

        'vs', 'core'
    ])

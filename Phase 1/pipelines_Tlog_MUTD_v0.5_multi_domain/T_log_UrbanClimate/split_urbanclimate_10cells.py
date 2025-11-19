import os
from copy import deepcopy

import nbformat


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTEBOOK_PATH = os.path.join(BASE_DIR, "T_log_UrbanClimate.ipynb")
OUT_DIR = os.path.join(BASE_DIR, "UrbanClimate_split_10cells")
OUT_PREFIX = "UrbanClimate_part"
CELLS_PER_PART = 10


def split_notebook_fixed_chunks(nb_path: str = NOTEBOOK_PATH,
                                cells_per_part: int = CELLS_PER_PART) -> None:
    """Split a notebook into fixed-size chunks of cells.

    The original notebook is left untouched. Parts are written under OUT_DIR
    with names OUT_PREFIX##.ipynb. The last part may contain fewer cells.
    """
    if not os.path.exists(nb_path):
        raise FileNotFoundError(f"Notebook not found: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    cells = nb.cells
    n = len(cells)

    os.makedirs(OUT_DIR, exist_ok=True)

    part_idx = 0
    for start in range(0, n, cells_per_part):
        end = min(start + cells_per_part, n)
        part_idx += 1

        part_cells = deepcopy(cells[start:end])
        new_nb = nbformat.v4.new_notebook()
        new_nb.cells = part_cells
        new_nb.metadata = deepcopy(getattr(nb, "metadata", {}))

        out_name = f"{OUT_PREFIX}{part_idx:02d}.ipynb"
        out_path = os.path.join(OUT_DIR, out_name)
        nbformat.write(new_nb, out_path)
        print(f"→ Wrote {out_path} (cells {start}–{end - 1})")

    print(
        f"Done: {part_idx} parts written in {OUT_DIR}/, "
        f"{cells_per_part} cells per part (last part may be shorter)."
    )


if __name__ == "__main__":
    split_notebook_fixed_chunks()

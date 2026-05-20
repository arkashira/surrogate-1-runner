import React, {
  useRef,
  useEffect,
  useCallback,
  KeyboardEvent,
  useState,
} from 'react';
import './InventoryGrid.css'; // see styles below

type InventoryGridProps<T> = {
  /** 2‑D array of data – each sub‑array is a row */
  data: T[][];
  /** Optional header row(s) – each sub‑array is a header row */
  headers?: string[][];
  /** Optional cell renderer – receives cell value, row index, col index */
  renderCell?: (
    value: T,
    rowIndex: number,
    colIndex: number
  ) => React.ReactNode;
};

export default function InventoryGrid<T>({
  data,
  headers = [],
  renderCell,
}: InventoryGridProps<T>) {
  const gridRef = useRef<HTMLTableElement>(null);
  const [selected, setSelected] = useState<{ row: number; col: number } | null>(
    null
  );

  /* ------------------------------------------------------------------ */
  /*  Keyboard navigation logic                                         */
  /* ------------------------------------------------------------------ */
  const focusCell = useCallback(
    (row: number, col: number) => {
      const grid = gridRef.current;
      if (!grid) return;
      const cell = grid.querySelectorAll('tbody td')[row * data[0].length + col];
      if (cell) {
        (cell as HTMLElement).focus();
        setSelected({ row, col });
      }
    },
    [data]
  );

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTableElement>) => {
      if (!selected) return;
      const { row, col } = selected;
      const colCount = data[0].length;
      const rowCount = data.length;

      let newRow = row;
      let newCol = col;

      switch (e.key) {
        case 'ArrowUp':
          newRow = Math.max(row - 1, 0);
          break;
        case 'ArrowDown':
          newRow = Math.min(row + 1, rowCount - 1);
          break;
        case 'ArrowLeft':
          newCol = Math.max(col - 1, 0);
          break;
        case 'ArrowRight':
          newCol = Math.min(col + 1, colCount - 1);
          break;
        case 'Home':
          newCol = 0;
          break;
        case 'End':
          newCol = colCount - 1;
          break;
        case 'PageUp':
          newRow = Math.max(row - 5, 0); // 5 rows per page
          break;
        case 'PageDown':
          newRow = Math.min(row + 5, rowCount - 1);
          break;
        default:
          return; // ignore other keys
      }

      e.preventDefault();
      focusCell(newRow, newCol);
    },
    [selected, data, focusCell]
  );

  /* ------------------------------------------------------------------ */
  /*  Initial focus – pick first cell if none selected                */
  /* ------------------------------------------------------------------ */
  useEffect(() => {
    if (!selected && data.length && data[0].length) {
      focusCell(0, 0);
    }
  }, [selected, data, focusCell]);

  /* ------------------------------------------------------------------ */
  /*  Render helpers                                                    */
  /* ------------------------------------------------------------------ */
  const cellContent = (value: T, r: number, c: number) =>
    renderCell ? renderCell(value, r, c) : value;

  return (
    <div className="inventory-grid-wrapper">
      <table
        ref={gridRef}
        className="inventory-grid"
        role="grid"
        onKeyDown={handleKeyDown}
        tabIndex={0}
      >
        {headers.length > 0 && (
          <thead>
            {headers.map((headerRow, hrIdx) => (
              <tr key={hrIdx}>
                {headerRow.map((header, hcIdx) => (
                  <th key={hcIdx} scope="col">
                    {header}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
        )}
        <tbody>
          {data.map((row, rIdx) => (
            <tr key={rIdx}>
              {row.map((cell, cIdx) => (
                <td
                  key={cIdx}
                  tabIndex={-1}
                  role="gridcell"
                  aria-selected={
                    selected?.row === rIdx && selected?.col === cIdx
                  }
                >
                  {cellContent(cell, rIdx, cIdx)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
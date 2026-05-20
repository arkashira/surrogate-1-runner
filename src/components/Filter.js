import React, { useState, useEffect } from "react";

/**
 * Props
 * -----
 * categories: string[]          // e.g. ["CPU", "GPU", "Motherboard"]
 * specs: string[]               // all spec keys that exist in the data set
 * onChange: (filterObj) => void // called on every UI change
 *
 * filterObj shape
 * ----------------
 * {
 *   category: string | null,
 *   minPrice: number | null,
 *   maxPrice: number | null,
 *   specs: { [specName]: string }   // empty string means “any”
 * }
 */
export default function Filter({ categories = [], specs = [], onChange }) {
  // ----- UI state ---------------------------------------------------------
  const [category, setCategory] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [specValues, setSpecValues] = useState({});

  // initialise specValues when the spec list changes
  useEffect(() => {
    const init = {};
    specs.forEach((s) => (init[s] = ""));
    setSpecValues(init);
  }, [specs]);

  // ----- Emit a fresh filter object whenever any field changes ------------
  useEffect(() => {
    const filter = {
      category: category || null,
      minPrice: minPrice ? Number(minPrice) : null,
      maxPrice: maxPrice ? Number(maxPrice) : null,
      specs: { ...specValues },
    };
    onChange && onChange(filter);
  }, [category, minPrice, maxPrice, specValues, onChange]);

  // ----- Helpers -----------------------------------------------------------
  const handleSpecChange = (spec, value) => {
    setSpecValues((prev) => ({ ...prev, [spec]: value }));
  };

  // ----- Render ------------------------------------------------------------
  return (
    <section
      className="filter-panel"
      style={{
        marginBottom: "1rem",
        padding: "1rem",
        border: "1px solid #ddd",
        borderRadius: "4px",
        backgroundColor: "#fafafa",
      }}
    >
      <h3 style={{ marginTop: 0 }}>Filter Components</h3>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          alignItems: "flex-end",
        }}
      >
        {/* Category selector */}
        <div>
          <label>
            Category
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{ marginLeft: "0.5rem" }}
            >
              <option value="">All</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
        </div>

        {/* Price range */}
        <div>
          <label>
            Min Price
            <input
              type="number"
              min="0"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
              placeholder="0"
              style={{ marginLeft: "0.5rem", width: "80px" }}
            />
          </label>
        </div>

        <div>
          <label>
            Max Price
            <input
              type="number"
              min="0"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              placeholder="∞"
              style={{ marginLeft: "0.5rem", width: "80px" }}
            />
          </label>
        </div>

        {/* Dynamic spec fields */}
        {specs.map((spec) => (
          <div key={spec}>
            <label>
              {spec}
              <input
                type="text"
                value={specValues[spec] || ""}
                onChange={(e) => handleSpecChange(spec, e.target.value)}
                placeholder="any"
                style={{ marginLeft: "0.5rem", width: "120px" }}
              />
            </label>
          </div>
        ))}
      </div>
    </section>
  );
}
import React, { useState, useEffect } from "react";
import Reviews from "./Reviews";

/**
 * ProductPage – shows a single product and lets the user filter its reviews.
 *
 * Props
 * -----
 * productId : string | number – the ID used by the backend API.
 *
 * Extensible: add more UI controls and push their values into `criteria`
 * without touching the Reviews component.
 */
const ProductPage = ({ productId }) => {
  // ----------------------------------------------------------------------
  // 1️⃣ Product data (once)
  // ----------------------------------------------------------------------
  const [product, setProduct] = useState(null);
  const [productError, setProductError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/products/${productId}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!cancelled) setProduct(data);
      })
      .catch((err) => {
        if (!cancelled) setProductError(err.message);
        console.error(err);
      });
    return () => {
      cancelled = true;
    };
  }, [productId]);

  // ----------------------------------------------------------------------
  // 2️⃣ Search / filter criteria (flexible)
  // ----------------------------------------------------------------------
  const [criteria, setCriteria] = useState({
    minRating: "",   // empty string = “any”
    search: "",      // free‑text search
    // future filters (price, brand, …) can be added here
  });

  const handleCriteriaChange = (e) => {
    const { name, value } = e.target;
    setCriteria((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ----------------------------------------------------------------------
  // 3️⃣ Render
  // ----------------------------------------------------------------------
  if (productError) {
    return <div className="error">Failed to load product: {productError}</div>;
  }

  if (!product) {
    return <div className="loading">Loading product…</div>;
  }

  return (
    <div className="product-page" style={{ maxWidth: "800px", margin: "auto" }}>
      {/* ---- Product header ------------------------------------------------ */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* ---- Criteria UI --------------------------------------------------- */}
      <div
        className="criteria-controls"
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          marginBottom: "1.5rem",
        }}
      >
        {/* Minimum rating */}
        <label>
          Minimum Rating:
          <select
            name="minRating"
            value={criteria.minRating}
            onChange={handleCriteriaChange}
            style={{ marginLeft: "0.5rem" }}
          >
            <option value="">Any</option>
            <option value="1">1★+</option>
            <option value="2">2★+</option>
            <option value="3">3★+</option>
            <option value="4">4★+</option>
            <option value="5">5★</option>
          </select>
        </label>

        {/* Free‑text search */}
        <label>
          Search Reviews:
          <input
            type="text"
            name="search"
            placeholder="keyword"
            value={criteria.search}
            onChange={handleCriteriaChange}
            style={{ marginLeft: "0.5rem" }}
          />
        </label>

        {/* Add more controls here – they will automatically flow into `criteria` */}
      </div>

      {/* ---- Reviews list --------------------------------------------------- */}
      <Reviews productId={productId} criteria={criteria} />
    </div>
  );
};

export default ProductPage;
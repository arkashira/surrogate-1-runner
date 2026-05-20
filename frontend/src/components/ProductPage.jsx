import React, { useState, useEffect } from "react";
import Reviews from "./Reviews";

/**
 * ProductPage component
 *
 * @param {{ productId: string|number, initialCriteria?: object }} props
 */
const ProductPage = ({ productId, initialCriteria = {} }) => {
  const [product, setProduct] = useState(null);
  const [criteria, setCriteria] = useState(initialCriteria);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // -----------------------------------------------------------------
  // 1️⃣ Fetch product details (mocked – replace with real API later)
  // -----------------------------------------------------------------
  useEffect(() => {
    let isMounted = true;
    const fetchProduct = async () => {
      try {
        // 👉 Replace this block with a real fetch call.
        const mockProduct = {
          id: productId,
          name: `Sample Product ${productId}`,
          description:
            "A great product for demonstration purposes. Replace with real data.",
          price: "$99.99",
        };
        if (isMounted) {
          setProduct(mockProduct);
          setLoading(false);
        }
      } catch (err) {
        if (isMounted) {
          setError(err);
          setLoading(false);
        }
      }
    };
    fetchProduct();
    return () => {
      isMounted = false;
    };
  }, [productId]);

  // -----------------------------------------------------------------
  // 2️⃣ UI – filter criteria (currently only minRating)
  // -----------------------------------------------------------------
  const handleRatingChange = (e) => {
    const rating = e.target.value;
    setCriteria((prev) => ({
      ...prev,
      minRating: rating ? Number(rating) : undefined,
    }));
  };

  // -----------------------------------------------------------------
  // 3️⃣ Render
  // -----------------------------------------------------------------
  if (loading) return <div>Loading product…</div>;
  if (error) return <div style={{ color: "red" }}>Failed to load product.</div>;

  return (
    <div className="product-page" style={{ padding: "1rem" }}>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>
        <strong>{product.price}</strong>
      </p>

      {/* ----- Filter UI ----- */}
      <div style={{ marginTop: "1rem" }}>
        <label>
          Minimum Rating:&nbsp;
          <select
            value={criteria.minRating ?? ""}
            onChange={handleRatingChange}
          >
            <option value="">Any</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                {n}★
              </option>
            ))}
          </select>
        </label>
      </div>

      {/* ----- Reviews (auto‑updates on criteria change) ----- */}
      <Reviews productId={productId} criteria={criteria} />
    </div>
  );
};

export default ProductPage;
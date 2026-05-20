// Replace the two-Area hack with this:
<Area 
  type="monotone" 
  dataKey="revenueUpper" 
  stroke="none" 
  fill="#3b82f6" 
  fillOpacity={0.1}
  baseValue={0} // This creates the band effect
/>
// Then add revenueLower as a second Area with fill="white" or use a proper range
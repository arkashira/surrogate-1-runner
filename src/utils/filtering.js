export const filterComponents = (components, filters) => {
  return components.filter((component) => {
    const matchesCpu = !filters.cpu || component.cpu.includes(filters.cpu);
    const matchesGpu = !filters.gpu || component.gpu.includes(filters.gpu);
    const matchesRam = !filters.ram || component.ram.includes(filters.ram);
    return matchesCpu && matchesGpu && matchesRam;
  });
};
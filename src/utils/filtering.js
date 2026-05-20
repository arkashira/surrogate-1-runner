function filterComponents(components, filters) {
    const { cpu, gpu, ram } = filters;
    return components.filter(component => {
        if (cpu && component.cpu !== cpu) return false;
        if (gpu && component.gpu !== gpu) return false;
        if (ram && component.ram !== ram) return false;
        return true;
    });
}

module.exports = {
    filterComponents
};
package com.example.cloudopt;

import java.util.List;
import java.util.stream.Collectors;

public final class VmRecommendationProvider implements RecommendationProvider<VirtualMachine> {

    @Override
    public List<Recommendation> recommend(VirtualMachine vm) {
        if (vm.getCpuUtilization() < 0.2 && vm.getMemoryUtilization() < 0.2) {
            return List.of(
                new Recommendation(
                    "Downsize VM " + vm.getId(),
                    "Current size: " + vm.getSize() + ", suggested: " + vm.getSuggestedSize(),
                    vm::downsize
                )
            );
        }
        return List.of();
    }
}
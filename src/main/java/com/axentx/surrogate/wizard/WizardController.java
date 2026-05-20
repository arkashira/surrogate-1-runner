package com.axentx.surrogate.wizard;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
@RequestMapping("/wizard")
public class WizardController {

    @GetMapping("/step1")
    public ModelAndView selectDataSource() {
        return new ModelAndView("wizard/step1");
    }

    @PostMapping("/step1")
    public ModelAndView configureIngestionOptions(@RequestParam String dataSource) {
        // Validate dataSource
        if (dataSource == null || dataSource.isEmpty()) {
            return new ModelAndView("redirect:/wizard/step1");
        }
        return new ModelAndView("wizard/step2").addObject("dataSource", dataSource);
    }

    @PostMapping("/step2")
    public ModelAndView reviewAndLaunch(@RequestParam String dataSource, @RequestParam String ingestionOptions) {
        // Validate ingestionOptions
        if (ingestionOptions == null || ingestionOptions.isEmpty()) {
            return new ModelAndView("redirect:/wizard/step2");
        }
        return new ModelAndView("wizard/step3").addObject("dataSource", dataSource).addObject("ingestionOptions", ingestionOptions);
    }

    @PostMapping("/step3")
    public ModelAndView launchWizard(@RequestParam String dataSource, @RequestParam String ingestionOptions) {
        // Final validation and launch logic
        if (dataSource == null || dataSource.isEmpty() || ingestionOptions == null || ingestionOptions.isEmpty()) {
            return new ModelAndView("redirect:/wizard/step3");
        }
        // Simulate launch and show summary
        ModelAndView modelAndView = new ModelAndView("wizard/summary");
        modelAndView.addObject("dataSource", dataSource);
        modelAndView.addObject("ingestionOptions", ingestionOptions);
        modelAndView.addObject("estimatedCost", "Estimated cost: $100"); // Placeholder for estimated cost calculation
        return modelAndView;
    }
}
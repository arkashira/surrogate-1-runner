package com.axentx.surrogate1.dashboard;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class DashboardController {

    @Autowired
    private CloudSpendService cloudSpendService;

    @GetMapping("/dashboard")
    public String dashboard(Model model, @RequestParam(required = false) String account, @RequestParam(required = false) String sortBy) {
        List<CloudSpend> spends;
        if (account != null) {
            spends = cloudSpendService.getSpendsByAccount(account);
        } else {
            spends = cloudSpendService.getAllSpends();
        }

        if (sortBy != null) {
            spends.sort((s1, s2) -> s1.getSortValue(sortBy).compareTo(s2.getSortValue(sortBy)));
        }

        model.addAttribute("spends", spends);
        model.addAttribute("account", account);
        model.addAttribute("sortBy", sortBy);
        return "dashboard";
    }
}
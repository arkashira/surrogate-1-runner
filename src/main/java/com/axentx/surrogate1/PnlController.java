package com.axentx.surrogate1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.axentx.surrogate1.service.PnlService;

@RestController
@RequestMapping("/api/pnl")
public class PnlController {

    private final PnlService pnlService;
    private final SimpMessagingTemplate messagingTemplate;

    @Autowired
    public PnlController(PnlService pnlService, SimpMessagingTemplate messagingTemplate) {
        this.pnlService = pnlService;
        this.messagingTemplate = messagingTemplate;
    }

    @GetMapping("/data")
    public PnlData getPnlData() {
        PnlData pnlData = pnlService.getPnlData();
        messagingTemplate.convertAndSend("/topic/pnl", pnlData);
        return pnlData;
    }
}
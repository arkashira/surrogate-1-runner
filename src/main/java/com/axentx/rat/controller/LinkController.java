package com.axentx.rat.controller;

import com.axentx.rat.service.LinkService;
import com.axentx.rat.dto.LinkRequest;
import com.axentx.rat.dto.LinkResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/rat")
public class LinkController {

    private final LinkService linkService;

    @Autowired
    public LinkController(LinkService linkService) {
        this.linkService = linkService;
    }

    @PostMapping("/link")
    public ResponseEntity<LinkResponse> initiateLink(@RequestBody LinkRequest linkRequest) {
        try {
            LinkResponse response = linkService.initiateLink(linkRequest);
            return ResponseEntity.ok(response);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(new LinkResponse(e.getMessage(), null));
        }
    }
}
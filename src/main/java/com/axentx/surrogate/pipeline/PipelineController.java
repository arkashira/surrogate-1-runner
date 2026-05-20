import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@Tag(name = "PipelineController", description = "Pipeline Controller")
public class PipelineController {

    @GetMapping("/pipelines")
    @Operation(summary = "Get all pipelines")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "OK"),
            @ApiResponse(responseCode = "500", description = "Internal Server Error")
    })
    public ResponseEntity<List<Pipeline>> getPipelines() {
        // TO DO: implement pipeline retrieval logic
        return ResponseEntity.ok(List.of());
    }

    @GetMapping("/pipelines/{pipelineId}")
    @Operation(summary = "Get pipeline details")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "OK"),
            @ApiResponse(responseCode = "404", description = "Not Found"),
            @ApiResponse(responseCode = "500", description = "Internal Server Error")
    })
    public ResponseEntity<Pipeline> getPipeline(@PathVariable String pipelineId) {
        // TO DO: implement pipeline details retrieval logic
        return ResponseEntity.notFound().build();
    }
}
package com.axentx.surrogate1;

import java.util.List;

public interface ContentOrganizationRepository {
    void deleteRecordedStream(String streamId);
    List<String> getRecordedStreams();
}
package com.axentx.surrogate.pipeline;

import com.axentx.surrogate.model.Pipeline;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

/**
 * Repository for {@link Pipeline} entities.
 *
 * Added method {@code countPipelinesPerUserCurrentMonth()} to retrieve the
 * number of pipelines each creator has run in the current calendar month.
 * The query is native SQL for performance and is grouped by the creator's
 * identifier. Results are projected onto {@link UserPipelineCount}.
 */
@Repository
public interface PipelineRepository extends JpaRepository<Pipeline, Long> {

    /**
     * Returns a list of user‑pipeline count pairs for the current month.
     *
     * <p>The query aggregates pipelines created between the start of the
     * current month (inclusive) and the start of the next month (exclusive),
     * grouping by the creator's identifier.</p>
     *
     * @return list of {@link UserPipelineCount} projections
     */
    @Query(value = """
        SELECT
            p.creator_id AS userId,
            COUNT(*)    AS pipelineCount
        FROM pipelines p
        WHERE p.created_at >= DATE_TRUNC('month', CURRENT_DATE)
          AND p.created_at <  DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
        GROUP BY p.creator_id
        """, nativeQuery = true)
    List<UserPipelineCount> countPipelinesPerUserCurrentMonth();

    /**
     * Projection interface used by {@link #countPipelinesPerUserCurrentMonth()}.
     * Spring Data will map each row of the native query onto this interface.
     */
    interface UserPipelineCount {
        /** Identifier of the user/creator. */
        String getUserId();

        /** Number of pipelines run by the user in the queried period. */
        Long getPipelineCount();
    }

    // -----------------------------------------------------------------------
    // Existing repository methods (if any) remain unchanged below.
    // -----------------------------------------------------------------------
}
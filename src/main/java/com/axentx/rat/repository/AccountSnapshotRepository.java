package com.axentx.rat.repository;

import com.axentx.rat.model.AccountSnapshot;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository for accessing {@link AccountSnapshot} entities.
 * <p>
 * Provides a paging method that returns snapshots ordered by {@code date} in descending order.
 */
@Repository
public interface AccountSnapshotRepository extends JpaRepository<AccountSnapshot, Long> {

    /**
     * Returns a page of {@link AccountSnapshot} entities ordered by {@code date} descending.
     *
     * @param pageable the pagination information (page number, size, sort)
     * @return a page of account snapshots
     */
    Page<AccountSnapshot> findAllByOrderByDateDesc(Pageable pageable);
}
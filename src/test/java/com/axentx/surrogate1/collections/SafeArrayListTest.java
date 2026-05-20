package com.axentx.surrogate1.collections;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class SafeArrayListTest {

    private SafeArrayList<Integer> safeList;
    private List<Integer> backingList;

    @BeforeEach
    void setUp() {
        backingList = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));
        safeList = new SafeArrayList<>(backingList);
    }

    @DisplayName("addAll adds all elements from the given collection")
    @Test
    void addAll_HappyPath_AddsElements() {
        List<Integer> toAdd = Arrays.asList(6, 7, 8);
        safeList.addAll(toAdd);

        assertEquals(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8), safeList);
    }

    @DisplayName("addAll with empty collection does not modify list")
    @Test
    void addAll_EmptyCollection_NoModification() {
        List<Integer> empty = Collections.emptyList();
        safeList.addAll(empty);

        assertEquals(Arrays.asList(1, 2, 3, 4, 5), safeList);
    }

    @DisplayName("addAll with null collection throws NullPointerException")
    @Test
    void addAll_NullCollection_ThrowsNPE() {
        assertThrows(NullPointerException.class, () -> safeList.addAll(null));
    }

    @DisplayName("addAll with null element in collection throws NullPointerException")
    @Test
    void addAll_ContainsNull_ThrowsNPE() {
        List<Integer> toAdd = Arrays.asList(6, null, 8);
        assertThrows(NullPointerException.class, () -> safeList.addAll(toAdd));
    }

    @DisplayName("removeIf removes elements matching predicate")
    @Test
    void removeIf_HappyPath_RemovesMatchingElements() {
        int removed = safeList.removeIf(x -> x % 2 == 0);

        assertEquals(2, removed);
        assertEquals(Arrays.asList(1, 3, 5), safeList);
    }

    @DisplayName("removeIf with no matching elements returns zero")
    @Test
    void removeIf_NoMatchingElements_ReturnsZero() {
        int removed = safeList.removeIf(x -> x == 100);

        assertEquals(0, removed);
        assertEquals(Arrays.asList(1, 2, 3, 4, 5), safeList);
    }

    @DisplayName("removeIf with null predicate throws NullPointerException")
    @Test
    void removeIf_NullPredicate_ThrowsNPE() {
        assertThrows(NullPointerException.class, () -> safeList.removeIf(null));
    }

    @DisplayName("removeIf with null element throws NullPointerException")
    @Test
    void removeIf_ContainsNull_ThrowsNPE() {
        safeList.add(null);
        assertThrows(NullPointerException.class, () -> safeList.removeIf(x -> x != null));
    }

    @DisplayName("replaceAll replaces elements matching predicate")
    @Test
    void replaceAll_HappyPath_ReplacesMatchingElements() {
        int replaced = safeList.replaceAll(x -> x % 2 == 0, x -> x * 10);

        assertEquals(2, replaced);
        assertEquals(Arrays.asList(1, 20, 3, 40, 5), safeList);
    }

    @DisplayName("replaceAll with no matching elements returns zero")
    @Test
    void replaceAll_NoMatchingElements_ReturnsZero() {
        int replaced = safeList.replaceAll(x -> x == 100, x -> x * 10);

        assertEquals(0, replaced);
        assertEquals(Arrays.asList(1, 2, 3, 4, 5), safeList);
    }

    @DisplayName("replaceAll with null predicate throws NullPointerException")
    @Test
    void replaceAll_NullPredicate_ThrowsNPE() {
        assertThrows(NullPointerException.class, () -> safeList.replaceAll(null, x -> x * 10));
    }

    @DisplayName("replaceAll with null replacement function throws NullPointerException")
    @Test
    void replaceAll_NullReplacementFunction_ThrowsNPE() {
        assertThrows(NullPointerException.class, () -> safeList.replaceAll(x -> x % 2 == 0, null));
    }

    @DisplayName("replaceAll with null element throws NullPointerException")
    @Test
    void replaceAll_ContainsNull_ThrowsNPE() {
        safeList.add(null);
        assertThrows(NullPointerException.class, () -> safeList.replaceAll(x -> x != null, x -> x * 10));
    }

    @DisplayName("addAll throws IllegalStateException when modifying during iteration")
    @Test
    void addAll_ModifyingDuringIteration_ThrowsIllegalStateException() {
        Iterator<Integer> iterator = safeList.iterator();
        iterator.next();

        assertThrows(IllegalStateException.class, () -> safeList.addAll(Arrays.asList(6)));
    }

    @DisplayName("removeIf throws IllegalStateException when modifying during iteration")
    @Test
    void removeIf_ModifyingDuringIteration_ThrowsIllegalStateException() {
        Iterator<Integer> iterator = safeList.iterator();
        iterator.next();

        assertThrows(IllegalStateException.class, () -> safeList.removeIf(x -> x % 2 == 0));
    }

    @DisplayName("replaceAll throws IllegalStateException when modifying during iteration")
    @Test
    void replaceAll_ModifyingDuringIteration_ThrowsIllegalStateException() {
        Iterator<Integer> iterator = safeList.iterator();
        iterator.next();

        assertThrows(IllegalStateException.class, () -> safeList.replaceAll(x -> x % 2 == 0, x -> x * 10));
    }

    @DisplayName("SafeArrayList constructor with null backing list throws NullPointerException")
    @Test
    void constructor_NullBackingList_ThrowsNPE() {
        assertThrows(NullPointerException.class, () -> new SafeArrayList<>(null));
    }

    @DisplayName("SafeArrayList constructor with null element in backing list throws NullPointerException")
    @Test
    void constructor_ContainsNullInBackingList_ThrowsNPE() {
        List<Integer> backingWithNull = Arrays.asList(1, null, 3);
        assertThrows(NullPointerException.class, () -> new SafeArrayList<>(backingWithNull));
    }
}
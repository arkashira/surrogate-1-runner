package com.axentx.surrogate1.collections;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.ListIterator;
import java.util.concurrent.ConcurrentModificationException;

public class SafeArrayList<E> extends ArrayList<E> {

    private int modCountCheck;

    @Override
    public boolean addAll(Collection<? extends E> c) {
        checkNull(c);
        modCountCheck = modCount;
        boolean result = super.addAll(c);
        checkModCount();
        return result;
    }

    @Override
    public boolean removeIf(java.util.function.Predicate<? super E> filter) {
        checkNull(filter);
        modCountCheck = modCount;
        boolean result = super.removeIf(filter);
        checkModCount();
        return result;
    }

    @Override
    public void replaceAll(java.util.function.UnaryOperator<E> operator) {
        checkNull(operator);
        modCountCheck = modCount;
        super.replaceAll(operator);
        checkModCount();
    }

    private void checkNull(Object obj) {
        if (obj == null) {
            throw new NullPointerException("Argument cannot be null");
        }
    }

    private void checkModCount() {
        if (modCount != modCountCheck) {
            throw new IllegalStateException("List modified during operation");
        }
    }

    @Override
    public Iterator<E> iterator() {
        return new SafeIterator<>(super.iterator());
    }

    @Override
    public ListIterator<E> listIterator() {
        return new SafeListIterator<>(super.listIterator());
    }

    private static class SafeIterator<E> implements Iterator<E> {
        private final Iterator<E> iterator;
        private int modCountCheck;

        public SafeIterator(Iterator<E> iterator) {
            this.iterator = iterator;
            this.modCountCheck = ((ArrayList<E>) iterator.getClass().getDeclaringClass().getDeclaredField("this$0").get(iterator)).modCount;
        }

        @Override
        public boolean hasNext() {
            return iterator.hasNext();
        }

        @Override
        public E next() {
            modCountCheck = ((ArrayList<E>) iterator.getClass().getDeclaredField("this$0").get(iterator)).modCount;
            return iterator.next();
        }

        @Override
        public void remove() {
            iterator.remove();
            checkModCount();
        }

        private void checkModCount() {
            if (((ArrayList<E>) iterator.getClass().getDeclaredField("this$0").get(iterator)).modCount != modCountCheck) {
                throw new IllegalStateException("List modified during iteration");
            }
        }
    }

    private static class SafeListIterator<E> implements ListIterator<E> {
        private final ListIterator<E> listIterator;
        private int modCountCheck;

        public SafeListIterator(ListIterator<E> listIterator) {
            this.listIterator = listIterator;
            this.modCountCheck = ((ArrayList<E>) listIterator.getClass().getDeclaredField("this$0").get(listIterator)).modCount;
        }

        @Override
        public boolean hasNext() {
            return listIterator.hasNext();
        }

        @Override
        public E next() {
            modCountCheck = ((ArrayList<E>) listIterator.getClass().getDeclaredField("this$0").get(listIterator)).modCount;
            return listIterator.next();
        }

        @Override
        public boolean hasPrevious() {
            return listIterator.hasPrevious();
        }

        @Override
        public E previous() {
            modCountCheck = ((ArrayList<E>) listIterator.getClass().getDeclaredField("this$0").get(listIterator)).modCount;
            return listIterator.previous();
        }

        @Override
        public int nextIndex() {
            return listIterator.nextIndex();
        }

        @Override
        public int previousIndex() {
            return listIterator.previousIndex();
        }

        @Override
        public void remove() {
            listIterator.remove();
            checkModCount();
        }

        @Override
        public void set(E e) {
            listIterator.set(e);
            checkModCount();
        }

        @Override
        public void add(E e) {
            listIterator.add(e);
            checkModCount();
        }

        private void checkModCount() {
            if (((ArrayList<E>) listIterator.getClass().getDeclaredField("this$0").get(listIterator)).modCount != modCountCheck) {
                throw new IllegalStateException("List modified during iteration");
            }
        }
    }
}
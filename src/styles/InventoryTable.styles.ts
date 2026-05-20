import styled from 'styled-components';

export const TableWrapper = styled.div`
  font-family: Arial, sans-serif;
  padding: 1rem;
`;

export const Filters = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  align-items: center;
`;

export const Select = styled.select`
  padding: 0.5rem;
  font-size: 1rem;
`;

export const Input = styled.input`
  padding: 0.5rem;
  font-size: 1rem;
  flex: 1;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  th,
  td {
    padding: 0.75rem;
    border: 1px solid #ddd;
  }
  th {
    background: #f5f5f5;
    text-align: left;
  }
`;

export const Pagination = styled.div`
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
`;

export const PageButton = styled.button<{ active?: boolean }>`
  padding: 0.5rem 0.75rem;
  border: none;
  background: ${({ active }) => (active ? '#007bff' : '#e9ecef')};
  color: ${({ active }) => (active ? '#fff' : '#000')};
  cursor: pointer;
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
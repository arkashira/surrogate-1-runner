import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';

interface Alternative {
  name: string;
  performance: number;
  price: number;
}

interface Props {
  alternatives: Alternative[];
}

const AlternativesComparison = ({ alternatives }: Props) => {
  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Performance</TableCell>
            <TableCell>Price</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {alternatives.map((alternative, index) => (
            <TableRow key={index}>
              <TableCell>{alternative.name}</TableCell>
              <TableCell>{alternative.performance}</TableCell>
              <TableCell>{alternative.price}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default AlternativesComparison;
import React from 'react';
import { List, ListItem } from '@material-ui/core';
import AlternativeCard from './AlternativeCard';

interface Props {
  alternatives: { name: string; performance: number; price: number }[];
}

const AlternativesList = ({ alternatives }: Props) => {
  return (
    <List>
      {alternatives.map((alternative, index) => (
        <ListItem key={index}>
          <AlternativeCard alternative={alternative} />
        </ListItem>
      ))}
    </List>
  );
};

export default AlternativesList;
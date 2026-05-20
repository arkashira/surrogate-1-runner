import React from 'react';
import { Card, CardContent } from '@material-ui/core';

interface Alternative {
  name: string;
  performance: number;
  price: number;
}

interface Props {
  alternative: Alternative;
}

const AlternativeCard = ({ alternative }: Props) => {
  return (
    <Card>
      <CardContent>
        <h2>{alternative.name}</h2>
        <p>Performance: {alternative.performance}</p>
        <p>Price: {alternative.price}</p>
      </CardContent>
    </Card>
  );
};

export default AlternativeCard;

import React, { useState } from 'react';
import { Form, Formik } from 'formik';
import * as Yup from 'yup';

const CostOptimizationPolicySchema = Yup.object().shape({
  ec2: Yup.number().min(0).max(100).required(),
  rds: Yup.number().min(0).max(100).required(),
  s3: Yup.number().min(0).max(100).required(),
});

const CostOptimizationPolicy = () => {
  const [policy, setPolicy] = useState({ ec2: 50, rds: 60, s3: 70 });

  const handleSubmit = (values) => {
    // Save policy to the backend
    console.log(values);
  };

  return (
    <div>
      <h1>Cost Optimization Policies</h1>
      <Formik
        initialValues={policy}
        validationSchema={CostOptimizationPolicySchema}
        onSubmit={handleSubmit}
      >
        {({ values, handleSubmit, handleChange, handleBlur }) => (
          <Form onSubmit={handleSubmit}>
            <label htmlFor="ec2">EC2</label>
            <input
              id="ec2"
              name="ec2"
              type="number"
              value={values.ec2}
              onChange={handleChange}
              onBlur={handleBlur}
            />

            <label htmlFor="rds">RDS</label>
            <input
              id="rds"
              name="rds"
              type="number"
              value={values.rds}
              onChange={handleChange}
              onBlur={handleBlur}
            />

            <label htmlFor="s3">S3</label>
            <input
              id="s3"
              name="s3"
              type="number"
              value={values.s3}
              onChange={handleChange}
              onBlur={handleBlur}
            />

            <button type="submit">Save</button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default CostOptimizationPolicy;
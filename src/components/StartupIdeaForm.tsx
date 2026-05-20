import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

interface StartupIdeaFormData {
  problem: string;
  solution: string;
  tam: number;
  sam: number;
  som: number;
  unitEconomics: string;
  competitiveAnalysis: string;
}

const schema = yup.object().shape({
  problem: yup.string().required('Problem statement is required'),
  solution: yup.string().required('Solution statement is required'),
  tam: yup.number().required('Total Addressable Market is required').min(0),
  sam: yup.number().required('Serviceable Available Market is required').min(0),
  som: yup.number().required('Serviceable Obtainable Market is required').min(0),
  unitEconomics: yup.string().required('Unit economics is required'),
  competitiveAnalysis: yup.string().required('Competitive analysis is required'),
});

const StartupIdeaForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<StartupIdeaFormData>({
    resolver: yupResolver(schema),
  });

  const onSubmit: SubmitHandler<StartupIdeaFormData> = (data) => {
    console.log(data);
    // Here you would typically send the data to your backend
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Problem Statement</label>
        <input {...register('problem')} />
        {errors.problem && <p>{errors.problem.message}</p>}
      </div>

      <div>
        <label>Solution Statement</label>
        <input {...register('solution')} />
        {errors.solution && <p>{errors.solution.message}</p>}
      </div>

      <div>
        <label>Total Addressable Market (TAM)</label>
        <input type="number" {...register('tam')} />
        {errors.tam && <p>{errors.tam.message}</p>}
      </div>

      <div>
        <label>Serviceable Available Market (SAM)</label>
        <input type="number" {...register('sam')} />
        {errors.sam && <p>{errors.sam.message}</p>}
      </div>

      <div>
        <label>Serviceable Obtainable Market (SOM)</label>
        <input type="number" {...register('som')} />
        {errors.som && <p>{errors.som.message}</p>}
      </div>

      <div>
        <label>Unit Economics</label>
        <textarea {...register('unitEconomics')} />
        {errors.unitEconomics && <p>{errors.unitEconomics.message}</p>}
      </div>

      <div>
        <label>Competitive Analysis</label>
        <textarea {...register('competitiveAnalysis')} />
        {errors.competitiveAnalysis && <p>{errors.competitiveAnalysis.message}</p>}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
};

export default StartupIdeaForm;
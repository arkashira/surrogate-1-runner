import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

function BrandProfile() {
    const { register, handleSubmit, errors } = useForm();

    const onSubmit = async (data) => {
        try {
            const response = await axios.post('/api/brands/', data);
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <label>
                Name:
                <input type="text" {...register('name', { required: true })} />
                {errors.name && <div>This field is required</div>}
            </label>
            <br />
            <label>
                Description:
                <textarea {...register('description', { required: true })} />
                {errors.description && <div>This field is required</div>}
            </label>
            <br />
            <label>
                Product Requirements:
                <textarea {...register('productRequirements', { required: true })} />
                {errors.productRequirements && <div>This field is required</div>}
            </label>
            <br />
            <label>
                Budget:
                <input type="number" {...register('budget', { required: true, valueAsNumber: true })} />
                {errors.budget && <div>This field is required</div>}
            </label>
            <br />
            <input type="submit" value="Create Brand Profile" />
        </form>
    );
}

export default BrandProfile;
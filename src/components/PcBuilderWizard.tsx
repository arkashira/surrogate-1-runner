import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Button, Typography } from '@material-ui/core';
import CpuSelection from './CpuSelection';
import GpuSelection from './GpuSelection';
import MotherboardSelection from './MotherboardSelection';
import RamSelection from './RamSelection';
import StorageSelection from './StorageSelection';
import PsuSelection from './PsuSelection';
import CaseSelection from './CaseSelection';
import AccessoriesSelection from './AccessoriesSelection';
import SummaryPage from './SummaryPage';

const steps = ['CPU', 'GPU', 'Motherboard', 'RAM', 'Storage', 'PSU', 'Case', 'Accessories', 'Summary'];

const PcBuilderWizard = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedComponents, setSelectedComponents] = useState({
    cpu: null,
    gpu: null,
    motherboard: null,
    ram: null,
    storage: null,
    psu: null,
    case: null,
    accessories: []
  });

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleComponentSelection = (componentType, component) => {
    setSelectedComponents((prevComponents) => ({
      ...prevComponents,
      [componentType]: component
    }));
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return <CpuSelection onSelect={(cpu) => handleComponentSelection('cpu', cpu)} />;
      case 1:
        return <GpuSelection onSelect={(gpu) => handleComponentSelection('gpu', gpu)} />;
      case 2:
        return <MotherboardSelection onSelect={(motherboard) => handleComponentSelection('motherboard', motherboard)} />;
      case 3:
        return <RamSelection onSelect={(ram) => handleComponentSelection('ram', ram)} />;
      case 4:
        return <StorageSelection onSelect={(storage) => handleComponentSelection('storage', storage)} />;
      case 5:
        return <PsuSelection onSelect={(psu) => handleComponentSelection('psu', psu)} />;
      case 6:
        return <CaseSelection onSelect={(caseItem) => handleComponentSelection('case', caseItem)} />;
      case 7:
        return <AccessoriesSelection onSelect={(accessories) => handleComponentSelection('accessories', accessories)} />;
      case 8:
        return <SummaryPage components={selectedComponents} />;
      default:
        return 'Unknown step';
    }
  };

  return (
    <div>
      <Stepper activeStep={activeStep}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <div>
        {activeStep === steps.length ? (
          <div>
            <Typography>All steps completed</Typography>
            <Button onClick={() => setActiveStep(0)}>Reset</Button>
          </div>
        ) : (
          <div>
            {getStepContent(activeStep)}
            <div>
              <Button disabled={activeStep === 0} onClick={handleBack}>
                Back
              </Button>
              <Button variant="contained" color="primary" onClick={handleNext}>
                {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PcBuilderWizard;
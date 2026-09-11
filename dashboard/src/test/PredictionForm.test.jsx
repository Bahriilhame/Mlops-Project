import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PredictionForm from '../components/PredictionForm';
import { FEATURE_GROUPS } from '../data/features';
import { predictStudent } from '../services/api';
vi.mock('../services/api', () => ({ predictStudent: vi.fn() }));

function fillAll() {
  for (let index = 0; index < FEATURE_GROUPS.length; index++) {
    for (const field of FEATURE_GROUPS[index].fields) fireEvent.change(document.getElementById(field.name), { target: { value: '0' } });
    if (index < 4) fireEvent.click(screen.getByRole('button', { name: /Continuer/ }));
  }
}

describe('Prediction form', () => {
  it('shows one organized section and prevents missing inputs', () => {
    render(<PredictionForm/>);
    expect(screen.getAllByRole('spinbutton')).toHaveLength(6);
    fireEvent.click(screen.getByRole('button', { name: /Continuer/ }));
    expect(screen.getAllByText('Ce champ est obligatoire.')).toHaveLength(6);
    expect(predictStudent).not.toHaveBeenCalled();
  });
  it('submits 34 numbers, prevents double submits and displays the result', async () => {
    let resolve;
    predictStudent.mockReturnValue(new Promise(done => { resolve = done; }));
    render(<PredictionForm/>);fillAll();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(predictStudent).not.toHaveBeenCalled();
    const button = screen.getByRole('button', { name: 'Predict Student Cluster' });
    fireEvent.click(button);fireEvent.submit(button.closest('form'));
    expect(predictStudent).toHaveBeenCalledTimes(1);
    expect(Object.keys(predictStudent.mock.calls[0][0])).toHaveLength(34);
    expect(screen.getByRole('button', { name: /Analyse en cours/ })).toBeDisabled();
    resolve({ cluster: 1, profile: 'Low-Engagement / At-Risk Learner' });
    await screen.findByText('Low-Engagement / At-Risk Learner');
    expect(screen.getByText('Cluster 1')).toBeInTheDocument();
    expect(screen.getByText(/pas une prédiction certaine/)).toBeInTheDocument();
    fireEvent.change(document.getElementById('late_submission_count'), { target: { value: '1' } });
    expect(screen.queryByText('Cluster 1')).not.toBeInTheDocument();
  });
  it('shows request errors and allows retry', async () => {
    predictStudent.mockRejectedValue(new Error('API inaccessible.'));
    render(<PredictionForm/>);fillAll();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(predictStudent).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Predict Student Cluster' }));
    await screen.findByRole('alert');
    await waitFor(() => expect(screen.getByRole('button', { name: 'Predict Student Cluster' })).toBeEnabled());
    expect(screen.getByRole('alert')).toHaveTextContent('API inaccessible.');
  });
});


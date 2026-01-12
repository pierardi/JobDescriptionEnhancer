import React, { useState } from 'react';
import './InterviewForm.css';

const InterviewForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    req_id: '',
    basic_title: '',
    basic_description: '',
    basic_department: '',
    basic_level: '',
    work_output: '',
    work_role: '',
    work_knowledge: '',
    work_competencies: '',
    interview_name: '',
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validate = () => {
    const newErrors = {};
    
    if (!formData.req_id.trim()) {
      newErrors.req_id = 'Requisition ID is required';
    }
    
    if (!formData.basic_title.trim()) {
      newErrors.basic_title = 'Job title is required';
    }
    
    if (!formData.basic_description.trim()) {
      newErrors.basic_description = 'Job description is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validate()) {
      // Generate interview name if not provided
      const submissionData = {
        ...formData,
        interview_name: formData.interview_name || `${formData.basic_title} Interview`,
      };
      onSubmit(submissionData);
    }
  };

  return (
    <form className="interview-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <h2>Job Description Details</h2>
        
        <div className="form-group">
          <label htmlFor="req_id">
            Requisition ID <span className="required">*</span>
          </label>
          <input
            type="text"
            id="req_id"
            name="req_id"
            value={formData.req_id}
            onChange={handleChange}
            placeholder="e.g., REQ-12345"
            className={errors.req_id ? 'error' : ''}
          />
          {errors.req_id && <span className="error-message">{errors.req_id}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="basic_title">
            Job Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="basic_title"
            name="basic_title"
            value={formData.basic_title}
            onChange={handleChange}
            placeholder="e.g., Senior Software Engineer"
            className={errors.basic_title ? 'error' : ''}
          />
          {errors.basic_title && <span className="error-message">{errors.basic_title}</span>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="basic_department">Department</label>
            <input
              type="text"
              id="basic_department"
              name="basic_department"
              value={formData.basic_department}
              onChange={handleChange}
              placeholder="e.g., Engineering"
            />
          </div>

          <div className="form-group">
            <label htmlFor="basic_level">Job Level</label>
            <select
              id="basic_level"
              name="basic_level"
              value={formData.basic_level}
              onChange={handleChange}
            >
              <option value="">Select level</option>
              <option value="Junior">Junior</option>
              <option value="Mid">Mid</option>
              <option value="Senior">Senior</option>
              <option value="Lead">Lead</option>
              <option value="Principal">Principal</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="basic_description">
            Job Description <span className="required">*</span>
          </label>
          <textarea
            id="basic_description"
            name="basic_description"
            value={formData.basic_description}
            onChange={handleChange}
            placeholder="Enter the job description..."
            rows="6"
            className={errors.basic_description ? 'error' : ''}
          />
          {errors.basic_description && (
            <span className="error-message">{errors.basic_description}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="interview_name">Interview Name</label>
          <input
            type="text"
            id="interview_name"
            name="interview_name"
            value={formData.interview_name}
            onChange={handleChange}
            placeholder="Auto-generated if left empty"
          />
        </div>
      </div>

      <div className="form-section">
        <h2>WORK Methodology Inputs</h2>
        <p className="help-text">
          These fields help create better, more targeted interview questions. They are optional but highly recommended.
        </p>

        <div className="form-group">
          <label htmlFor="work_output">
            Work Output
            <span className="help-icon" title="What will this person deliver/build?">ℹ️</span>
          </label>
          <textarea
            id="work_output"
            name="work_output"
            value={formData.work_output}
            onChange={handleChange}
            placeholder="e.g., Design and build microservices that handle 10,000 transactions per second with real-time fraud detection"
            rows="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="work_role">
            Work Role
            <span className="help-icon" title="What are the key responsibilities?">ℹ️</span>
          </label>
          <textarea
            id="work_role"
            name="work_role"
            value={formData.work_role}
            onChange={handleChange}
            placeholder="e.g., Lead backend architecture, mentor junior engineers, own service reliability and performance"
            rows="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="work_knowledge">
            Work Knowledge
            <span className="help-icon" title="What knowledge areas are critical?">ℹ️</span>
          </label>
          <textarea
            id="work_knowledge"
            name="work_knowledge"
            value={formData.work_knowledge}
            onChange={handleChange}
            placeholder="e.g., Kafka/RabbitMQ, PostgreSQL/NoSQL, Spring Boot, distributed systems, load balancing, API design"
            rows="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="work_competencies">
            Work Competencies
            <span className="help-icon" title="What competencies are essential?">ℹ️</span>
          </label>
          <textarea
            id="work_competencies"
            name="work_competencies"
            value={formData.work_competencies}
            onChange={handleChange}
            placeholder="e.g., System design, problem solving, technical depth, communication, mentorship"
            rows="3"
          />
        </div>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Creating Interview...' : 'Create Interview'}
        </button>
        <button
          type="button"
          className="btn-secondary"
          onClick={() => setFormData({
            req_id: '',
            basic_title: '',
            basic_description: '',
            basic_department: '',
            basic_level: '',
            work_output: '',
            work_role: '',
            work_knowledge: '',
            work_competencies: '',
            interview_name: '',
          })}
          disabled={loading}
        >
          Clear Form
        </button>
      </div>
    </form>
  );
};

export default InterviewForm;
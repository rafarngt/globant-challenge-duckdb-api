CREATE TABLE IF NOT EXISTS hired_employees (
    id INTEGER, -- Id of the employee
    name VARCHAR, -- Name and surname of the employee
    hire_datetime VARCHAR, -- Hire datetime in ISO format
    department_id INTEGER, -- Id of the department which the employee was hired for
    job_id INTEGER -- Id of the job which the employee was hired for
);

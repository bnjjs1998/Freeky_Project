// InputField.tsx
import React from 'react';

interface InputFieldProps {
    label: string;
    type: string;
    name: string;
    value: string;
    onChange: (value: string) => void;
}

const InputField: React.FC<InputFieldProps> = ({ label, type, name, value, onChange }) => {
    return (
        <div>
            <label htmlFor={name}>{label}:</label>
            <input
                type={type}
                id={name}
                name={name}
                value={value}
                onChange={(e) => onChange(e.target.value)}
            />
        </div>
    );
};

export default InputField;

import * as React from 'react';

import { InputLabel, MenuItem, Select } from '@material-ui/core';

/**
 *
 * @param props {{onClick: (id: number) => void; options: string[]}}
 * @returns {JSX.Element}
 * @constructor
 */
export const DataPreparation = (props) => (
    <div>
        <h2>Предварительная обработка данных</h2>
        <div>Выберите опции предварительной обработки данных</div>
        <Select
            labelId="prep-option-select"
            onChange={(e) => {
                props.onClick(Number(e.target.value));
            }}
        >
            {props.options.map((item, idx) => (
                <MenuItem key={`select-${idx}`} value={idx}>{item}</MenuItem>
            ))}
        </Select>
    </div>
);
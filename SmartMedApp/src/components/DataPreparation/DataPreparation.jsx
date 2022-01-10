import * as React from 'react';

import * as s from './DataPreparation.scss';

import {MenuItem, Select} from '@material-ui/core';

/**
 *
 * @param props {{onClick: (id: number) => void; options: string[]}}
 * @returns {JSX.Element}
 * @constructor
 */
export const DataPreparation = (props) => (
    <div className={s.dataPreparation}>
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

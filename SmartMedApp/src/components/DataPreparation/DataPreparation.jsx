import * as React from 'react';

import * as s from './DataPreparation.scss';

import {FormControl, FormHelperText, InputLabel, MenuItem, Select} from '@material-ui/core';

/**
 *
 * @param props {{onClick: (id: number) => void; options: string[]}}
 * @returns {JSX.Element}
 * @constructor
 */
export const DataPreparation = (props) => (
    <div className={s.dataPreparation}>
        <FormControl required sx={{m: 1, minWidth: 120}}>
            <InputLabel id="prep-option-select-label">{props.labelName}</InputLabel>
            <Select
                labelId="prep-option-select-label"
                defaultValue={props.defaultValue}
                id="prep-option-select"
                label={<span style={{fontSize: '10px'}}>{props.labelName}</span>}
                onChange={(e) => {
                    props.onClick(Number(e.target.value));
                }}
            >
                {props.options.map((item, idx) => (
                    <MenuItem key={`select-${idx}`} value={idx}>{item}</MenuItem>
                ))}
            </Select>
            <FormHelperText>Обязательное поле</FormHelperText>
        </FormControl>
    </div>
);

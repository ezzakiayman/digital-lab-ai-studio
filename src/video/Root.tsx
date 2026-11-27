import React from 'react';
import {Composition} from 'remotion';
import {Lesson} from './Lesson';
import data from './demo-lesson.json';
import {duration,timelineSchema} from '../lib/timeline';
const timeline=timelineSchema.parse(data);
export const Root=()=> <Composition id="DigitalLab" component={Lesson} width={1920} height={1080} fps={30} durationInFrames={duration(timeline)} defaultProps={{timeline}} calculateMetadata={({props})=>{const t=timelineSchema.parse(props.timeline);return {durationInFrames:duration(t),props:{timeline:t}};}}/>;

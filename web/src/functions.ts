import Color from 'color';
import { defaultTagColor } from './constants';

export function adjustTagColorStyle(colorHex: string | undefined): string {
	const color = Color(colorHex || defaultTagColor);

	const accent = color.saturate(0.1).lightness(45);
	const backgorund = color.saturate(-0.2).lightness(90);

	return `border: 2px solid ${accent.hex()}; background-color: ${backgorund.hex()}; color: ${accent.hex()};`;
}

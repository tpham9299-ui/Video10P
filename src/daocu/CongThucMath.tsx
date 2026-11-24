import React, { useMemo } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

type CongThucMathProps = {
  latex: string;
  displayMode?: boolean;
  fontSize?: number;
  mau?: string;
};

export const CongThucMath: React.FC<CongThucMathProps> = ({
  latex,
  displayMode = true,
  fontSize = 44,
  mau = '#F8FAFC',
}) => {
  const ketQua = useMemo(() => {
    try {
      const html = katex.renderToString(latex, {
        displayMode,
        throwOnError: true,
        strict: false,
      });
      return { ok: true as const, html };
    } catch {
      return { ok: false as const, html: '' };
    }
  }, [latex, displayMode]);

  if (!ketQua.ok) {
    return (
      <div
        style={{
          color: '#FDE047',
          fontSize: Math.max(20, fontSize * 0.65),
          fontFamily: 'Consolas, monospace',
          padding: '8px 14px',
          border: '1px dashed #FDE047',
          borderRadius: 8,
        }}
      >
        {latex}
      </div>
    );
  }

  return (
    <div
      style={{
        color: mau,
        fontSize,
        lineHeight: 1.35,
      }}
      dangerouslySetInnerHTML={{ __html: ketQua.html }}
    />
  );
};

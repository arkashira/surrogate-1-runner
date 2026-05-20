import { createCanvas, loadImage } from 'canvas';
import { getMonthlySpend, getTopCostDrivers, getSavingsInsights } from './cost-utils';
import { PDFDocument } from 'pdf-lib';

interface ReportData {
  monthlySpend: number;
  topCostDrivers: { name: string; cost: number }[];
  savingsInsights: string;
}

async function generateReport(data: ReportData): Promise<Buffer> {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage();

  const font = await pdfDoc.embedFont('Helvetica');
  page.setFont(font);

  page.drawText(`Monthly Spend: $${data.monthlySpend}`, { x: 100, y: 700, size: 24 });
  page.drawText('Top Cost Drivers:', { x: 100, y: 650, size: 18 });

  let y = 600;
  for (const driver of data.topCostDrivers) {
    page.drawText(`${driver.name}: $${driver.cost}`, { x: 100, y: y, size: 18 });
    y -= 30;
  }

  page.drawText('Savings Insights:', { x: 100, y: 400, size: 18 });
  page.drawText(data.savingsInsights, { x: 100, y: 350, size: 18 });

  const pdfBytes = await pdfDoc.save();
  return pdfBytes;
}

export async function createPdfReport(): Promise<Buffer> {
  const monthlySpend = await getMonthlySpend();
  const topCostDrivers = await getTopCostDrivers();
  const savingsInsights = await getSavingsInsights();

  const reportData: ReportData = {
    monthlySpend,
    topCostDrivers,
    savingsInsights,
  };

  return generateReport(reportData);
}
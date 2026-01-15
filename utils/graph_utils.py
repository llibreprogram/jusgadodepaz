# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from controllers.case_controller import CaseController
from utils.responsive_utils import get_responsive_helper

class GraphUtils:
    def __init__(self):
        self.controller = CaseController()
        self.responsive = get_responsive_helper()
    
    def create_responsive_figure(self, width_ratio=0.4, height_ratio=0.3):
        """
        Create a matplotlib figure that adapts to screen DPI and resolution
        
        Args:
            width_ratio (float): Ratio of screen width to use (default: 0.4)
            height_ratio (float): Ratio of screen height to use (default: 0.3)
        
        Returns:
            tuple: (fig, ax) matplotlib figure and axes
        """
        # Get screen metrics
        screen_width, screen_height = self.responsive.get_screen_resolution()
        dpi = self.responsive.get_screen_dpi()
        
        # Calculate container size in pixels
        container_width = int(screen_width * width_ratio)
        container_height = int(screen_height * height_ratio)
        
        # Convert to inches for matplotlib
        width_inches = container_width / dpi
        height_inches = container_height / dpi
        
        # Create figure with responsive size and DPI
        fig, ax = plt.subplots(figsize=(width_inches, height_inches), dpi=dpi)
        
        return fig, ax

    def plot_resolved_vs_pending(self):
        stats = self.controller.get_statistics()
        labels = ['Resueltos', 'Pendientes']
        sizes = [stats['resolved'], stats['pending']]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title('Casos Resueltos vs Pendientes')
        plt.show(block=False)

    def plot_cases_by_category(self):
        stats = self.controller.get_statistics()
        categories = list(stats['cases_by_category'].keys())
        counts = list(stats['cases_by_category'].values())
        fig, ax = plt.subplots()
        ax.bar(categories, counts)
        ax.set_title('Casos por Categoría')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show(block=False)

    def plot_cases_per_month(self):
        stats = self.controller.get_statistics()
        months = list(stats['cases_per_month'].keys())
        counts = list(stats['cases_per_month'].values())
        if not months:
            fig, ax = plt.subplots()
            ax.set_title('Sin datos para mostrar')
            plt.show(block=False)
            return
        fig, ax = plt.subplots()
        ax.plot(months, counts, marker='o')
        ax.set_title('Casos por Mes')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.pause(0.001)
        plt.show(block=False)

    def plot_cases_by_estado(self):
        stats = self.controller.get_statistics()
        estados = list(stats['cases_by_estado'].keys())
        counts = list(stats['cases_by_estado'].values())
        fig, ax = plt.subplots()
        ax.bar(estados, counts, color='#22c55e')
        ax.set_title('Casos por Estado Actual')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show(block=False)

    def plot_appeals_ratio(self):
        stats = self.controller.get_statistics()
        appeals = stats.get('appeal_count', 0)
        total = stats.get('pending', 0) + stats.get('resolved', 0)
        fig, ax = plt.subplots()
        if total == 0:
            ax.set_title('Sin datos para mostrar')
            plt.show(block=False)
            return
        appeals = min(appeals, total)
        no_appeal = max(total - appeals, 0)
        labels = ['Apelados', 'Sin apelación']
        sizes = [appeals, no_appeal]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title('Proporción de apelaciones')
        plt.show(block=False)
    
    def plot_distribution_by_area(self):
        """Gráfico de distribución por área (Pensión, Tránsito, Otros)"""
        from views.main_window import MainWindow
        
        # Get cases and group by area
        cases = self.controller.get_all_cases()
        areas = {
            'Pensión Alimentaria': 0,
            'Tránsito': 0,
            'Otros Casos': 0
        }
        
        for case in cases:
            category_lower = case.categoria.lower() if case.categoria else ''
            if 'pensión' in category_lower or 'pension' in category_lower:
                areas['Pensión Alimentaria'] += 1
            elif 'tránsito' in category_lower or 'transito' in category_lower:
                areas['Tránsito'] += 1
            else:
                areas['Otros Casos'] += 1
        
        # Create pie chart
        labels = list(areas.keys())
        sizes = list(areas.values())
        colors = ['#10b981', '#f59e0b', '#8b5cf6']  # Verde, Naranja, Púrpura
        
        fig, ax = self.create_responsive_figure(width_ratio=0.45, height_ratio=0.35)
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        
        # Beautify with responsive font sizes
        base_font = self.responsive.scale_font_size(12)
        title_font = self.responsive.scale_font_size(16)
        
        for text in texts:
            text.set_fontsize(base_font)
            text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(base_font - 1)
            autotext.set_weight('bold')
        
        ax.set_title('Distribución de Casos por Área', fontsize=title_font, weight='bold', pad=20)
        plt.tight_layout()
        plt.show(block=False)
    
    def plot_resolution_types(self):
        """Gráfico de barras con tipos de resolución"""
        cases = self.controller.get_all_cases()
        
        resolution_types = {
            'Conciliaciones': 0,
            'Condenas': 0,
            'Acuerdos': 0,
            'No acuerdos': 0,
            'Desistimientos': 0,
            'Archivos': 0,
            'En proceso': 0
        }
        
        for case in cases:
            cat_lower = case.categoria.lower() if case.categoria else ''
            if 'conciliación' in cat_lower or 'conciliacion' in cat_lower:
                resolution_types['Conciliaciones'] += 1
            elif 'condena' in cat_lower:
                resolution_types['Condenas'] += 1
            elif 'acuerdo' in cat_lower and 'no acuerdo' not in cat_lower:
                resolution_types['Acuerdos'] += 1
            elif 'no acuerdo' in cat_lower:
                resolution_types['No acuerdos'] += 1
            elif 'desistimiento' in cat_lower:
                resolution_types['Desistimientos'] += 1
            elif 'archivo' in cat_lower:
                resolution_types['Archivos'] += 1
            else:
                resolution_types['En proceso'] += 1
        
        # Create bar chart
        labels = list(resolution_types.keys())
        counts = list(resolution_types.values())
        colors = ['#10b981', '#ef4444', '#3b82f6', '#f59e0b', '#8b5cf6', '#64748b', '#06b6d4']
        
        fig, ax = self.create_responsive_figure(width_ratio=0.5, height_ratio=0.35)
        bars = ax.bar(labels, counts, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars with responsive font
        label_font = self.responsive.scale_font_size(11)
        axis_font = self.responsive.scale_font_size(12)
        title_font = self.responsive.scale_font_size(16)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=label_font, weight='bold')
        
        ax.set_ylabel('Cantidad de Casos', fontsize=axis_font, weight='bold')
        ax.set_title('Tipos de Resolución de Casos', fontsize=title_font, weight='bold', pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show(block=False)

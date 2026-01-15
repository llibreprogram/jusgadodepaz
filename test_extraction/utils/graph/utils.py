import matplotlib.pyplot as plt
from controllers.case_controller import CaseController

class GraphUtils:
    def __init__(self):
        self.controller = CaseController()

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
        
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        
        # Beautify
        for text in texts:
            text.set_fontsize(12)
            text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
        
        ax.set_title('Distribución de Casos por Área', fontsize=16, weight='bold', pad=20)
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
        
        fig, ax = plt.subplots(figsize=(12, 7))
        bars = ax.bar(labels, counts, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=11, weight='bold')
        
        ax.set_ylabel('Cantidad de Casos', fontsize=12, weight='bold')
        ax.set_title('Tipos de Resolución de Casos', fontsize=16, weight='bold', pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show(block=False)

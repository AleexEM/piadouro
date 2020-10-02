class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        if not self.page_title:
            raise Exception('Page title not defined!')
        return self.page_title

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = self.get_page_title()
        return context

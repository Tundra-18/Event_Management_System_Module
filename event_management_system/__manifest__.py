{
    "name": "Event Management System",
    "website": "togzawyenaung@gmail.com",
    "category": "Productivity",
    "summary": "To manage and control events!",
    "author": "Zaw Ye Naung",
    "application": True,
    "version": "1.0",
    "depends": ['base'],
    "installable": True,
    "data":
    [
        "security/ir.model.access.csv",
        "views/event_views.xml",
        "views/host_views.xml",
        "views/event_form.xml",
        "views/event_views_tree.xml",
        "views/participated_list_line_views.xml",
        "views/participant_views.xml",
        "views/participated_list_views.xml",
        "views/participant_form.xml",
        "views/participant_views_tree.xml",
        "views/sponsor_views.xml",
        "views/agreement_list_line.xml",
        "views/sponsor_form.xml",
        "views/sponsor_agreement_views.xml",
        "views/sponsor_agreement_form.xml",
        "views/participated_list_form.xml",
        "views/sponsor_views_tree.xml",


        "views/event_views_kanban.xml",
        "views/sponsor_views_kanban.xml",
        "views/participant_views_kanban.xml",
        "views/host_form.xml",
        "views/host_views_tree.xml",
        "views/host_views_kanban.xml",
    ],

    'assets': {
        'web.assets_backend': [
            'event_management_system/static/src/css/style.css',
            'event_management_system/static/src/js/buttons.js',
        ],
}


}
export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        name: 'Главная',
        to: '/dashboard/',
        icon: 'cil-speedometer'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Онтологии',
        to: '/ontologies/',
        icon: 'cil-basket'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Пользователи',
        to: '/users/',
        icon: 'cil-user'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'О программе',
        to: '/about/',
        icon: 'cil-settings'
      },
    ]
  }
]
